from loader import bot
from telebot.types import CallbackQuery, InputMediaPhoto
from keyboards.inline.create_photo_buttons import create_photo_buttons


@bot.callback_query_handler(func=lambda elem: "PHOTO" in elem.data)
def create_photo_buttons_callback(call: CallbackQuery) -> None:
    action = call.data.split(",")[0].split("_")[0]
    index = int(call.data.split(",")[1])
    hotel_index = int(call.data.split(",")[2])

    with bot.retrieve_data(call.from_user.id) as data:
        if action == "PREV":
            if index == 0:
                new_index = len(data['search'][f"{data.get('search').get('mode')}"]['results']\
                            [hotel_index].get('hotel_photos')) - 1
            else:
                new_index = index - 1
            new_url = data['search'][f"{data.get('search').get('mode')}"]['results'][hotel_index].get('hotel_photos')[new_index]
            bot.edit_message_media(media=InputMediaPhoto(new_url),
                                   chat_id=call.from_user.id,
                                   message_id=call.message.message_id,
                                   reply_markup=create_photo_buttons(index=new_index, hotel_index=hotel_index))
        else:
            if index + 1 == len(data['search'][f"{data.get('search').get('mode')}"]['results']\
                            [hotel_index].get('hotel_photos')):
                new_index = 0
            else:
                new_index = index + 1
            new_url = data['search'][f"{data.get('search').get('mode')}"]['results']\
                            [hotel_index].get('hotel_photos')[new_index]
            bot.edit_message_media(media=InputMediaPhoto(new_url),
                                   chat_id=call.from_user.id,
                                   message_id=call.message.message_id,
                                   reply_markup=create_photo_buttons(index=new_index, hotel_index=hotel_index))
