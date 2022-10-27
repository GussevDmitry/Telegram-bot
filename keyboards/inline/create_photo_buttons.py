import json


def create_photo_buttons(index: int, hotel_index: int) -> json:
    """
    Creating the buttons "<" and ">" to scroll photos using inline keyboard
    :param index: photo url's index in the list of hotel's photos, storing in memory storage
    :param hotel_index: the hotel's identification number
    :return: json-file containing the buttons with specified callback
    """
    keyboard_photos = {"inline_keyboard": []}
    row = [
        {"text": "<", "callback_data": f"PREV_PHOTO,{index},{hotel_index}"},
        {"text": ">", "callback_data": f"NEXT_PHOTO,{index},{hotel_index}"}
    ]

    keyboard_photos["inline_keyboard"].append(row)

    return json.dumps(keyboard_photos)


def create_photo_buttons_history(index: int, hotel_index: int) -> json:
    """
    Creating the buttons "<" and ">" to scroll photos (history command is chosen) using inline keyboard
    :param index: photo url's index in the list of hotel's photos, storing in memory storage after collecting
    urls from database (table Photo)
    :param hotel_index: the hotel's identification number
    :return: json-file containing the buttons with specified callback
    """
    keyboard_photos = {"inline_keyboard": []}
    row = [
        {"text": "<", "callback_data": f"PREV_HIST,{index},{hotel_index}"},
        {"text": ">", "callback_data": f"NEXT_HIST,{index},{hotel_index}"}
    ]

    keyboard_photos["inline_keyboard"].append(row)

    return json.dumps(keyboard_photos)
