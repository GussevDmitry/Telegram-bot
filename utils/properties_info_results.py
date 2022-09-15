import json
from typing import List
from utils.get_correct_price import get_correct_price
from utils.get_API_info import get_info


def check_the_dist_and_the_price(results: List, total_results: List, hotels_count: int, data) -> List:
    # Checking the hotel price
    for i_hotel in results:
        if len(total_results) < hotels_count:
            i_hotel_pr_str = get_correct_price(i_item_dict=i_hotel)  # '2,500 RUB'
            i_hotel_pr = i_hotel_pr_str.split()[0].replace(',', '')
            if '.' in i_hotel_pr:
                i_hotel_price = float(i_hotel_pr)
            else:
                i_hotel_price = int(i_hotel_pr)

            start_pr = data.get('search').get('bestdeal').get('price_range')[0]
            stop_pr = data.get('search').get('bestdeal').get('price_range')[1]
            if start_pr <= i_hotel_price <= stop_pr:

                # Checking the hotel distance
                for i_lms in i_hotel.get('landmarks'):
                    res = float(i_lms.get('distance').split()[0])
                    start_dist = data.get('search').get('bestdeal').get('distance_range')[0]
                    stop_dist = data.get('search').get('bestdeal').get('distance_range')[1]
                    if start_dist <= res <= stop_dist:
                        total_results.append(
                            i_hotel
                        )
                        break
        else:
            return total_results


def properties_info_results(data) -> List:
    hotels_count = data.get('hotels_count')
    slice_count = hotels_count % 25
    total_results = []

    if data.get('search').get('mode') != 'bestdeal':
        request_count = data.get('request_count')

        for i_req in range(1, request_count + 1):
            data['querystring_properties_list']['pageNumber'] = str(i_req)
            data['querystring_properties_list']['pageSize'] = "25"

            properties_info_lp = get_info(url='https://hotels4.p.rapidapi.com/properties/list',
                                          querystring=data['querystring_properties_list'])

            with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt", 'w', encoding='utf-8') as file:
                file.write(properties_info_lp)

            with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt", 'r', encoding='utf-8') as file:
                temp_data = file.read()
            result = json.loads(f"{temp_data}")
            results = result.get('data').get('body').get('searchResults').get('results')

            if len(results) == 0:
                total_results.append("По Вашему запросу ничего не найдено. Давайте попробуем изменить запрос.")
                return total_results

            if i_req == request_count:
                total_results.extend(results[:slice_count])
            else:
                total_results.extend(results)

        """Запись в json"""
        with open(f"parced_data/properties_info_{data.get('search').get('mode')}.json", 'w', encoding="utf-8") as file:
            json.dump(total_results, file, indent=4)

        return total_results

    else:
        i_req = 1
        while hotels_count > len(total_results):
            print(i_req)
            data['querystring_properties_list']['pageNumber'] = str(i_req)
            data['querystring_properties_list']['pageSize'] = "25"
            print(data)

            properties_info_lp = get_info(url='https://hotels4.p.rapidapi.com/properties/list',
                                          querystring=data['querystring_properties_list'])
            i_req += 1

            with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt", 'w',
                      encoding='utf-8') as file:
                file.write(properties_info_lp)

            with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt", 'r', encoding='utf-8') as file:
                temp_data = file.read()
            result = json.loads(f"{temp_data}")
            results = result.get('data').get('body').get('searchResults').get('results')

            if len(results) == 0:
                total_results.append("По Вашему запросу ничего не найдено. Давайте попробуем изменить запрос.")
                return total_results


            total_results = check_the_dist_and_the_price(results=results,
                                                         total_results=total_results,
                                                         hotels_count=hotels_count,
                                                         data=data)
            print(total_results)

        """Запись в json"""
        with open(f"parced_data/properties_info_{data.get('search').get('mode')}.json", 'w', encoding='utf-8') as file:
            json.dump(total_results, file, indent=4)

        return total_results