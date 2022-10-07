from loader import bot
from telebot.types import CallbackQuery
from states.user_states import UserStateInfo


@bot.callback_query_handler(func=lambda call: call.data in ['USD', 'EUR', 'RUB'])
def currency(call: CallbackQuery) -> None:
    """
    Handling the callback (function "currency_choice") with preferred currency.
    Asking user in which city he/she prefers to search hotels
    :param call: user's currency choice
    """
    bot.answer_callback_query(callback_query_id=call.id, text='Запомнил!')
    if call.data == "USD":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'].update(
                {'currency': 'USD'}
            )
            data['querystring_properties_list'].update(
                {'currency': 'USD'}
            )
            data['currency'] = ("долларов США", "доллар США", "доллара США", "долларах США")

    elif call.data == "EUR":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'].update(
                {'currency': 'EUR'}
            )
            data['querystring_properties_list'].update(
                {'currency': 'EUR'}
            )
            data['currency'] = ("евро", "евро", "евро", "евро")

    elif call.data == "RUB":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'].update(
                {'currency': 'RUB'}
            )
            data['querystring_properties_list'].update(
                {'currency': 'RUB'}
            )
            data['currency'] = ("рублей", "рубль", "рубля", "рублях")

    bot.send_message(call.message.chat.id, f"Запомнил. Теперь введите на {data.get('language')} языке "
                                           "в каком городе будем вести поиск отелей.")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.set_state(call.from_user.id, UserStateInfo.search_city)
