from loader import bot
from telebot.types import CallbackQuery, InputMediaPhoto
from keyboards.inline.create_photo_buttons import create_photo_buttons, create_photo_buttons_history


@bot.callback_query_handler(func=lambda elem: "PHOTO" in elem.data)
def create_photo_buttons_callback(call: CallbackQuery) -> None:
    """
    Handling the callback (function "create_photo_buttons") with user's preferred option (scrolling left or right)
    :param call: user's preferred option (scrolling left or right)
    """
    action = call.data.split(",")[0].split("_")[0]
    index = int(call.data.split(",")[1])
    hotel_index = int(call.data.split(",")[2])

    with bot.retrieve_data(call.from_user.id) as data:
        search_mode = data.get('search').get('mode')
        if action == "PREV":
            if index == 0:
                new_index = len(data['search'][f"{search_mode}"]['results'][hotel_index].get('hotel_photos')) - 1
            else:
                new_index = index - 1
            new_url = data['search'][f"{search_mode}"]['results'][hotel_index].get('hotel_photos')[new_index]
            bot.edit_message_media(media=InputMediaPhoto(new_url),
                                   chat_id=call.from_user.id,
                                   message_id=call.message.message_id,
                                   reply_markup=create_photo_buttons(index=new_index, hotel_index=hotel_index))
        else:
            if index + 1 == len(data['search'][f"{search_mode}"]['results'][hotel_index].get('hotel_photos')):
                new_index = 0
            else:
                new_index = index + 1
            new_url = data['search'][f"{search_mode}"]['results'][hotel_index].get('hotel_photos')[new_index]
            bot.edit_message_media(media=InputMediaPhoto(new_url),
                                   chat_id=call.from_user.id,
                                   message_id=call.message.message_id,
                                   reply_markup=create_photo_buttons(index=new_index, hotel_index=hotel_index))


@bot.callback_query_handler(func=lambda elem: "HIST" in elem.data)
def create_photo_buttons_history_callback(call: CallbackQuery) -> None:
    """
    Handling the callback (function "create_photo_buttons_history") with user's preferred option
    (scrolling left or right). History command is chosen
    :param call: user's preferred option (scrolling left or right)
    """
    action = call.data.split(",")[0].split("_")[0]
    index = int(call.data.split(",")[1])
    hotel_index = int(call.data.split(",")[2])

    with bot.retrieve_data(call.from_user.id) as data:
        if action == "PREV":
            if index == 0:
                new_index = len(data.get("history_urls").get(f"{hotel_index}")) - 1
            else:
                new_index = index - 1
            new_url = data.get("history_urls").get(f"{hotel_index}")[new_index]
            bot.edit_message_media(media=InputMediaPhoto(new_url),
                                   chat_id=call.from_user.id,
                                   message_id=call.message.message_id,
                                   reply_markup=create_photo_buttons_history(index=new_index, hotel_index=hotel_index))
        else:
            if index + 1 == len(data.get("history_urls").get(f"{hotel_index}")):
                new_index = 0
            else:
                new_index = index + 1
            new_url = data.get("history_urls").get(f"{hotel_index}")[new_index]
            bot.edit_message_media(media=InputMediaPhoto(new_url),
                                   chat_id=call.from_user.id,
                                   message_id=call.message.message_id,
                                   reply_markup=create_photo_buttons_history(index=new_index, hotel_index=hotel_index))
