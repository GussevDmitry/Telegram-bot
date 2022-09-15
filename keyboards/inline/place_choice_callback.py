from loader import bot
from telebot.types import CallbackQuery
from keyboards.reply.start_search import start_search
from handlers.lowprice.lowprice import lowprice_search
from handlers.highprice.highprice import highprice_search
from handlers.bestdeal.bestdeal import bestdeal_search


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def choose_place(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id) as data:
        data['querystring_properties_list'].update(
            {'destinationId' : str(call.data)}
        )
        if data.get('search').get('mode') == 'bestdeal':
            data['search'][f"{data.get('search').get('mode')}"].update(
                {
                    'header': call.data
                }
            )
        else:
            data['search'].update(
                {
                    f"{data.get('search').get('mode')}": {
                        'header': call.data
                    }
                }
            )

        data['search'][f"{data.get('search').get('mode')}"].update(
            {
                'results': []
            }
        )

    bot.send_message(call.from_user.id, "Нажмите на кнопку для начала поиска.", reply_markup=start_search())
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    if data.get('search').get('mode') == 'lowprice':
        data['querystring_properties_list'].update(
            {'sortOrder' : 'PRICE'}
        )
        bot.register_next_step_handler(call.message, lowprice_search)
    elif data.get('search').get('mode') == 'highprice':
        data['querystring_properties_list'].update(
            {'sortOrder': 'PRICE_HIGHEST_FIRST'}
        )
        bot.register_next_step_handler(call.message, highprice_search)
    else:
        data['querystring_properties_list'].update(
            {'sortOrder': 'DISTANCE_FROM_LANDMARK'}
        )
        bot.register_next_step_handler(call.message, bestdeal_search)