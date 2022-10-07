import json
import re


def location_info_results(location_info: str) -> json:
    """
    Searching the "CITY_GROUP" key in response from API
    :param location_info: response from API
    :return: json file containing the information about city groups
    """
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, location_info)
    if find:
        location_info_result = json.loads(f"{{{find[0]}}}")
        return location_info_result
