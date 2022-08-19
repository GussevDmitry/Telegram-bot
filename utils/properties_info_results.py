import json
from pprint import pprint
from typing import List
from utils.get_correct_price import get_correct_price

def properties_info_results(data) -> List:
    with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt", 'r') as file:
        temp_data = file.read()
    result = json.loads(f"{temp_data}")
    results = result.get('data').get('body').get('searchResults').get('results')

    """Запись в json"""
    with open(f"parced_data/properties_info_{data.get('search').get('mode')}.json", 'w') as file:
        json.dump(results, file, indent=4)

    if data.get('search').get('mode') != 'bestdeal':
        return results

    results_to_show = []

    """Checking the price"""
    for i_hotel in results:
        i_hotel_pr_str = get_correct_price(i_item_dict=i_hotel)  # '2,500 RUB'
        i_hotel_pr = i_hotel_pr_str.split()[0].replace(',', '')
        if '.' in i_hotel_pr:
            i_hotel_price = float(i_hotel_pr)
        else:
            i_hotel_price = int(i_hotel_pr)

        start_pr = data.get('search').get('bestdeal').get('price_range')[0]
        stop_pr = data.get('search').get('bestdeal').get('price_range')[1]
        if start_pr <= i_hotel_price <= stop_pr:
            """Checking the distance"""
            for i_lms in i_hotel.get('landmarks'):
                res = float(i_lms.get('distance').split()[0])
                start_dist = data.get('search').get('bestdeal').get('distance_range')[0]
                stop_dist = data.get('search').get('bestdeal').get('distance_range')[1]
                if start_dist <= res <= stop_dist:
                    results_to_show.append(
                        i_hotel
                    )
                    pprint(results_to_show)
    return results_to_show