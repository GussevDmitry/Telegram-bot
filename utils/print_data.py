from utils.misc.commands_comparison import commands_comparison


def print_data(data):
    search_mode = data.get('search').get('mode')
    desc = commands_comparison(mode=search_mode)
    text = f"{desc}\n" \
           f"Ищем отель в городе: {data.get('querystring_location_search').get('query').title()}\n" \
           f"Стоимость выводим в {data.get('currency')[3]}\n" \
           f"Даты с {data.get('querystring_properties_list').get('checkIn')} по " \
           f"{data.get('querystring_properties_list').get('checkOut')}\n" \
           f"Всего дней - {data.get('days_count')}\n" \
           f"Показываю отелей: {data.get('hotels_count')}\n"
    return text
