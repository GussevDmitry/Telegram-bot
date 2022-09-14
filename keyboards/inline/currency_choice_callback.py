from loader import bot
from telebot.types import CallbackQuery
from handlers.choice_collector import choose_rooms_count


@bot.callback_query_handler(func=lambda call: call.data in ['USD', 'EUR', 'RUB'])
def currency(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Запомнил!')
    if call.data == "USD":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'].update(
                {'currency': 'USD'}
            )
            data['querystring_properties_list'].update(
                {'currency': 'USD'}
            )

    elif call.data == "EUR":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'].update(
                {'currency': 'EUR'}
            )
            data['querystring_properties_list'].update(
                {'currency': 'EUR'}
            )

    elif call.data == "RUB":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'].update(
                {'currency': 'RUB'}
            )
            data['querystring_properties_list'].update(
                {'currency': 'RUB'}
            )
    bot.send_message(call.message.chat.id, "Запомнил. Теперь введите на АНГЛИЙСКОМ ЯЗЫКЕ "
                                           "в каком городе будем вести поиск отелей.")
    bot.register_next_step_handler(call.message, choose_rooms_count)