from states.user_states import UserStateInfo
from loader import bot
from telebot.types import Message

@bot.message_handler(state=UserStateInfo.info_collected, commands=['lowprice'])
def get_name(message: Message) -> None:
    bot.send_message(message.from_user.id, "")