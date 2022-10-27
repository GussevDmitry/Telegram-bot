import json
from typing import List, Dict
from utils.get_correct_price import get_correct_price
from utils.get_API_info import get_info
from loguru import logger


def check_the_dist_and_the_price(results: List, total_results: List, hotels_count: int, data: Dict) -> List:
    """
    Checking the distance from hotel to city centre and comparing with user's desired distance.
    Checking the hotel price and comparing with user's desired price
    :param results: the list, containing collected hotels with full information from response from API
    :param total_results: the list with appropriate hotels
    :param hotels_count: the amount of hotels that user would like to browse (from memory storage - data)
    :param data: memory storage
    :return: the list with appropriate hotels
    """
    # Checking the hotel price
    for i_hotel in results:
        if len(total_results) < hotels_count:
            i_hotel_pr = get_correct_price(i_item_dict=i_hotel, data=data)
            if isinstance(i_hotel_pr, str):
                continue

            start_pr = data.get('search').get('bestdeal').get('price_range')[0]
            stop_pr = data.get('search').get('bestdeal').get('price_range')[1]

            if start_pr <= i_hotel_pr <= stop_pr:
                # Checking the hotel distance
                start_dist = data.get('search').get('bestdeal').get('distance_range')[0]
                stop_dist = data.get('search').get('bestdeal').get('distance_range')[1]
                res = float(i_hotel.get('landmarks')[0].get('distance').split()[0].replace(',', '.'))
                if data.get('language') == 'английском':
                    start_dist /= 1.6093
                    stop_dist /= 1.6093

                if start_dist <= res <= stop_dist:
                    total_results.append(
                        i_hotel
                    )
        else:
            return total_results


def properties_info_results(data: Dict) -> List | str:
    """
    Collecting the list of appropriate for requirements hotels
    :param data: memory storage
    :return: the list of appropriate for requirements hotels or string if appropriate for requirements
    hotels are not found
    """
    hotels_count = data.get('hotels_count')
    slice_count = hotels_count % 25
    total_results = []

    if data.get('search').get('mode') != 'bestdeal':  # search mode in ("lowprice", "highprice")
        request_count = data.get('request_count')
        results_to_add = []

        for i_req in range(1, request_count + 1):
            data['querystring_properties_list']['pageNumber'] = str(i_req)
            data['querystring_properties_list']['pageSize'] = "25"

            properties_info_lp = get_info(url='https://hotels4.p.rapidapi.com/properties/list',
                                          querystring=data['querystring_properties_list'])
            print(properties_info_lp)

            with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt",
                      'w', encoding='utf-8') as file:
                file.write(properties_info_lp)

            with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt",
                      'r', encoding='utf-8') as file:
                temp_data = file.read()
            result = json.loads(f"{temp_data}")
            results = result.get('data').get('body').get('searchResults').get('results')

            if len(results) == 0:
                total_results = "По Вашему запросу ничего не найдено. Давайте попробуем изменить запрос."
                return total_results

            for i_hotel in results:
                if isinstance(get_correct_price(i_item_dict=i_hotel, data=data), int):
                    results_to_add.append(i_hotel)

            if i_req == request_count:
                total_results.extend(results_to_add[:slice_count])
            else:
                total_results.extend(results_to_add)

        """Запись в json"""
        with open(f"parced_data/properties_info_{data.get('search').get('mode')}.json", 'w', encoding="utf-8") as file:
            json.dump(total_results, file, indent=4)

        return total_results

    else:  # search mode is bestdeal
        i_req = 1
        while hotels_count > len(total_results):
            logger.debug(f"{i_req}")  # checking the amount of requests to API
            data['querystring_properties_list']['pageNumber'] = str(i_req)
            data['querystring_properties_list']['pageSize'] = "25"
            logger.debug(f"{data}")  # checking the memory storage (data)

            properties_info_lp = get_info(url='https://hotels4.p.rapidapi.com/properties/list',
                                          querystring=data['querystring_properties_list'])
            i_req += 1

            with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt",
                      'w', encoding='utf-8') as file:
                file.write(properties_info_lp)

            with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt",
                      'r', encoding='utf-8') as file:
                temp_data = file.read()
            result = json.loads(f"{temp_data}")
            results = result.get('data').get('body').get('searchResults').get('results')

            if len(results) == 0:
                total_results = "По Вашему запросу ничего не найдено. Давайте попробуем изменить запрос."
                return total_results

            total_results = check_the_dist_and_the_price(results=results,
                                                         total_results=total_results,
                                                         hotels_count=hotels_count,
                                                         data=data)
            print(total_results)

        # writing the information in json file
        with open(f"parced_data/properties_info_{data.get('search').get('mode')}.json", 'w', encoding='utf-8') as file:
            json.dump(total_results, file, indent=4)

        return total_results
