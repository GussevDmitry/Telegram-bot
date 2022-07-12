import telebot
import help, lowprice, highprice, bestdeal, history
from telebot import types
import json


name = ''
surname = ''
age = 0

database = []


def telegram_bot(token):
    bot = telebot.TeleBot(token=token)

    @bot.message_handler(commands=['start', 'hello-world'])
    def welcome(message):
        bot.send_message(message.chat.id, "Приветствую! Я помогу Вам подобрать отель для Вас! "
                                          "Давайте сначала познакомимся!")
        bot.send_message(message.chat.id, "Назовите Ваше имя?")
        bot.register_next_step_handler(message, get_name)


    def get_name(message):
        global name
        name = message.text
        bot.send_message(message.chat.id, "Назовите Вашу фамилию?")
        bot.register_next_step_handler(message, get_surname)


    def get_surname(message):
        global surname
        surname = message.text
        bot.send_message(message.from_user.id, "Сколько Вам лет?")
        bot.register_next_step_handler(message, get_age)


    def get_age(message):
        global age
        try:
            age = int(message.text)
        except Exception as _ex:
            bot.send_message(message.from_user.id, "Введите, пожалуйста, цифрами.")

        keyboard = types.InlineKeyboardMarkup()
        key_y = types.InlineKeyboardButton("Да", callback_data="yes")
        key_n = types.InlineKeyboardButton("Нет", callback_data="no")
        keyboard.add(key_y)
        keyboard.add(key_n)
        bot.send_message(message.from_user.id, f"Вас зовут {surname} {name} и Вам {age} лет?", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        if call.data == 'yes':
            database.append(
                {
                    'name': name,
                    'surname': surname,
                    'age': age,
                    'search_history': {}
                }
            )
            bot.send_message(call.message.chat.id, "Запомню :)")

        else:
            bot.send_message(call.message.chat.id, "Хм...странно. Попробуем еще раз. Введите команду /start")


    @bot.message_handler(content_types=['text'])
    def send_message(message):
        if message.text.lower() == '/help':
            bot.send_message(message.chat.id, help.print_info())
        elif message.text.lower() == '/lowprice':
            bot.send_message(message.chat.id, lowprice.print_info())
        elif message.text.lower() == '/highprice':
            bot.send_message(message.chat.id, highprice.print_info())
        elif message.text.lower() == '/bestdeal':
            bot.send_message(message.chat.id, bestdeal.print_info())
        elif message.text.lower() == '/history':
            bot.send_message(message.chat.id, history.print_info())
        else:
            bot.send_message(message.chat.id, "[ИНФО] Ого...я пока не знаю такого...Для начала работы наберите команду /start. "
                                              "Для получения информации по моим командам, наберите команду /help")


    bot.polling(non_stop=True, interval=0)