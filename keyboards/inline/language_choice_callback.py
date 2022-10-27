from loader import bot
from telebot.types import CallbackQuery
from keyboards.inline.currency_choice import currency_choice


@bot.callback_query_handler(func=lambda call: call.data in ('русский', 'английский'))
def language(call: CallbackQuery) -> None:
    """
    Catching the callback (function "language_choice") with preferred language
    :param call: user's language choice
    """
    bot.answer_callback_query(callback_query_id=call.id, text='Запомнил!')
    if call.data == "русский":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'] = {
                'locale': 'ru_RU'
            }
            data['querystring_properties_list'] = {
                'locale': 'ru_RU'
            }
            data['language'] = "русском"
    elif call.data == "английский":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'] = {
                'locale': 'en_US'
            }
            data['querystring_properties_list'] = {
                'locale': 'en_US'
            }
            data['language'] = "английском"
    bot.send_message(call.message.chat.id, "Теперь выберете в какой валюте выводить стоимость отелей.",
                     reply_markup=currency_choice())
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
