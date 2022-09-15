def currency_output(price: str, data) -> str:
    if price.endswith(("0", "5", "6", "7", "8", "9")):
        currency = data.get("currency")[0]
    elif price.endswith("1"):
        currency = data.get("currency")[1]
    else:
        currency = data.get("currency")[2]

    return currency