import json


def create_photo_buttons(index, hotel_index):
    keyboard_photos = {"inline_keyboard": []}
    row = [
        {"text": "<", "callback_data": f"PREV_PHOTO,{index},{hotel_index}"},
        {"text": ">", "callback_data": f"NEXT_PHOTO,{index},{hotel_index}"}
    ]

    keyboard_photos["inline_keyboard"].append(row)

    return json.dumps(keyboard_photos)