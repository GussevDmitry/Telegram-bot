from loader import bot
from telebot.types import CallbackQuery
from keyboards.inline.currency_choice import currency_choice


@bot.callback_query_handler(func=lambda call: call.data in ['ru-RU', 'en-US'])
def language(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Запомнил!')
    if call.data == "ru-RU":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'] = {
                'locale': 'ru-RU'
            }
            data['querystring_properties_list'] = {
                'locale': 'ru-RU'
            }
    elif call.data == "en-US":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'] = {
                'locale': 'en-US'
            }
            data['querystring_properties_list'] = {
                'locale': 'en-US'
            }
    bot.send_message(call.message.chat.id, "Теперь выберете в какой валюте выводить стоимость отелей.",
                     reply_markup=currency_choice())