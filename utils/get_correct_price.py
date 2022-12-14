import re
from typing import Dict


def get_correct_price(i_item_dict: Dict, data: Dict) -> int | str:
    """
    Getting the full price accommodation from information about hotel
    :param i_item_dict: full information about exact hotel
    :param data: memory storage
    :return: the full price accommodation or string if the full price is not mentioned
    """
    patterns = [r'\d{1,}[,.]+?\d{1,}[,.]+?\d{1,}[,.]+?\d{1,}', r'\d{1,}[,.]+?\d{1,}[,.]+?\d{1,}',
                r'\d{1,}[,.]+?\d{1,}', r'\d{1,}']
    try:
        if data.get("language") == "английском":
            total_price = i_item_dict.get('ratePlan').get('price').get('fullyBundledPricePerStay')
            for i_pat in patterns:
                res_pr = re.search(i_pat, total_price)
                if res_pr:
                    return int(res_pr.group(0).replace(',', ''))
            else:
                return "Стоимость недоступна..."
        else:
            price_per_night = i_item_dict.get('ratePlan').get('price').get('exactCurrent')
            nights = data.get("days_count")
            total_price = int(nights * price_per_night)
            return total_price

    except AttributeError:
        return "Стоимость недоступна..."
    except TypeError:
        return "Стоимость недоступна..."
