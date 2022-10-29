from typing import Dict


def currency_output(price: int, data: Dict) -> str:
    """
    Choosing the correct case for price description
    :param price: total accommodation price
    :param data: memory storage
    :return: correct case for price description
    """
    if str(price).endswith(("0", "5", "6", "7", "8", "9")):
        currency = data.get("currency")[0]
    elif str(price).endswith("1"):
        currency = data.get("currency")[1]
    elif str(price).endswith(("2", "3", "4")):
        currency = data.get("currency")[2]
    else:
        currency = ""

    return currency
