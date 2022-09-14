from loader import bot
from telebot.types import CallbackQuery
from datetime import datetime
from keyboards.inline.create_calendar import create_calendar
from handlers.choice_collector import get_hotels_count


@bot.callback_query_handler(func=lambda call: 'DAY' in call.data)
def callback_day(call: CallbackQuery) -> None:
    separator = call.data.rfind(";")
    day = call.data[separator + 1:]
    date_now = datetime.now().date()
    with bot.retrieve_data(call.from_user.id) as data:
        if data.get('querystring_properties_list').get('checkIn') is None:
            check_in = datetime(data.get("shown_dates")[0], data.get("shown_dates")[1], int(day)).date()
            if check_in >= date_now:
                data['querystring_properties_list'].update(
                    {'checkIn': str(check_in)}
                )
            else:
                bot.answer_callback_query(call.id, f"Выберете месяц и день не раньше сегодняшнего - {date_now}")
        else:
            check_out = datetime(data.get("shown_dates")[0], data.get("shown_dates")[1], int(day)).date()
            if datetime.fromisoformat(data.get('querystring_properties_list').get('checkIn')).date() <= check_out:
                data['querystring_properties_list'].update(
                    {'checkOut': str(check_out)}
                )
                check_in = datetime.fromisoformat(data.get('querystring_properties_list').get('checkIn')).date()
                delta = (check_out - check_in).days
                data['days_count'] = delta
                bot.send_message(call.from_user.id, "Введите какое количество отелей показать.")
                bot.register_next_step_handler(call.message, get_hotels_count)
            else:
                bot.answer_callback_query(call.id, f"Выберете месяц и день после даты заезда - "
                                                   f"{data.get('querystring_properties_list').get('checkIn')}")



@bot.callback_query_handler(func=lambda call: "MONTH" in call.data)
def callback_month(call: CallbackQuery) -> None:
    option = call.data.split(";")[0].split("_")[0]
    new_year, new_month = int(call.data.split(";")[1]), int(call.data.split(";")[2])

    if option == "PREV":
        if new_month == 1:
            new_month = 12
            new_year -= 1
        else:
            new_month -= 1
    else:
        if new_month == 12:
            new_month = 1
            new_year += 1
        else:
            new_month += 1

    with bot.retrieve_data(call.from_user.id) as data:
        data["shown_dates"] = (new_year, new_month)

    bot.edit_message_text("Выберете дату заезда/выезда.", call.from_user.id, call.message.message_id,
                          reply_markup=create_calendar(new_year, new_month))


@bot.callback_query_handler(func=lambda call: "IGNORE" in call.data)
def ignore_callback(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id, "Выберете месяц и день.", show_alert=True)