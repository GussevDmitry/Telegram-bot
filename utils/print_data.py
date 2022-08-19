def print_data(data):
    text = f"Ищем отель в городе: {data.get('querystring_location_search').get('query').title()}\n" \
           f"Стоимость выводим в валюте: {data.get('querystring_properties_list').get('currency')}\n" \
           f"Даты с {data.get('querystring_properties_list').get('checkIn')} по " \
           f"{data.get('querystring_properties_list').get('checkOut')}\n" \
           f"Всего дней - {int(data.get('days_count').days)}\n" \
           f"Показываю отелей: {data.get('querystring_properties_list').get('pageSize')}\n"
    return text