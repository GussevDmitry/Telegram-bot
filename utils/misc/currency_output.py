def currency_output(price: int, data) -> str:
    if str(price).endswith(("0", "5", "6", "7", "8", "9")):
        currency = data.get("currency")[0]
    elif str(price).endswith("1"):
        currency = data.get("currency")[1]
    elif str(price).endswith(("2", "3", "4")):
        currency = data.get("currency")[2]
    else:
        currency = ""

    return currency